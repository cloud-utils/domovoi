import os, inspect

import attr, boto3
import chalice.deploy.models
from chalice.deploy.packager import LambdaDeploymentPackager
from chalice.cli.factory import create_botocore_session

import domovoi


class DomovoiDeploymentPackager(LambdaDeploymentPackager):
    _CHALICE_LIB_DIR = "domovoilib"

    def _add_app_files(self, zip_fileobj, project_dir):
        domovoi_router = inspect.getfile(domovoi.app)
        if domovoi_router.endswith(".pyc"):
            domovoi_router = domovoi_router[:-1]
        zip_fileobj.write(domovoi_router, "domovoi/app.py")

        domovoi_init = inspect.getfile(domovoi)
        if domovoi_init.endswith(".pyc"):
            domovoi_init = domovoi_init[:-1]
        zip_fileobj.write(domovoi_init, "domovoi/__init__.py")

        chalice_router = inspect.getfile(chalice.app)
        if chalice_router.endswith(".pyc"):
            chalice_router = chalice_router[:-1]
        zip_fileobj.write(chalice_router, "chalice/app.py")

        chalice_init = inspect.getfile(chalice)
        if chalice_init.endswith(".pyc"):
            chalice_init = chalice_init[:-1]
        zip_fileobj.write(chalice_init, "chalice/__init__.py")

        zip_fileobj.write(os.path.join(project_dir, "app.py"), "app.py")
        self._add_chalice_lib_if_needed(project_dir, zip_fileobj)

    def _needs_latest_version(self, filename):
        return filename == 'app.py' or filename.startswith(('domovoilib/', 'domovoi/'))

    def create_deployment_package(self, project_dir, python_version, package_filename=None):
        deployment_package_filename = self.deployment_package_filename(project_dir, python_version)
        if os.path.exists(deployment_package_filename):
            self.inject_latest_app(deployment_package_filename, project_dir)
            return deployment_package_filename
        else:
            return LambdaDeploymentPackager.create_deployment_package(self, project_dir, python_version,
                                                                      package_filename=package_filename)


@attr.attrs
class ManagedIAMRole(chalice.deploy.models.ManagedIAMRole):
    def __attrs_post_init__(self):
        self.role_name = self.role_name.rpartition("-")[0]


@attr.attrs
class LambdaFunction(chalice.deploy.models.LambdaFunction):
    def __attrs_post_init__(self):
        self.function_name = self.function_name.rpartition("-")[0]


def patch_chalice():
    chalice.deploy.packager.LambdaDeploymentPackager = DomovoiDeploymentPackager
    chalice.deploy.deployer.LambdaDeploymentPackager = DomovoiDeploymentPackager
    chalice.deploy.models.ManagedIAMRole = ManagedIAMRole
    chalice.deploy.models.LambdaFunction = LambdaFunction


def add_filter_config(event_config, event_handler):
    cfg = dict(event_config)
    for fltr in "prefix", "suffix":
        if event_handler.get(fltr):
            cfg.setdefault("Filter", dict(Key=dict(FilterRules=[])))
            cfg["Filter"]["Key"]["FilterRules"].append(dict(Name=fltr, Value=event_handler[fltr]))
    return cfg


def get_boto3_session(user_agent_extra, profile, debug):
    botocore_session = create_botocore_session(profile=profile, debug=debug)
    botocore_session.user_agent_extra = user_agent_extra
    return boto3.session.Session(botocore_session=botocore_session)


class DomovoiLambdaManager:
    def __init__(self, function_name, awslambda_client):
        self.function_name = function_name
        self.awslambda = awslambda_client

    def put_event_source_mapping(self, event_source_arn, source_data, dry_run=False):
        event_source_mapping_args = dict(EventSourceArn=event_source_arn,
                                         FunctionName=self.function_name,
                                         Enabled=True)
        if "dynamodb" in event_source_arn:
            event_source_mapping_args.update(StartingPosition="TRIM_HORIZON")
        if source_data["batch_size"] is not None:
            event_source_mapping_args.update(BatchSize=source_data["batch_size"])
        esm = None
        try:
            if not dry_run:
                esm = self.awslambda.create_event_source_mapping(**event_source_mapping_args)
        except self.awslambda.exceptions.ResourceConflictException as e:
            assert "already exists" in str(e) and str(e).split()[-2] == "UUID"
            if source_data["batch_size"] is not None:
                esm_uuid = str(e).split()[-1]
                esm = self.awslambda.get_event_source_mapping(UUID=esm_uuid)
                if source_data["batch_size"] != esm["BatchSize"]:
                    esm = self.awslambda.update_event_source_mapping(UUID=esm_uuid, BatchSize=source_data["batch_size"])
        return esm
