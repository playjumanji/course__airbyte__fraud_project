import os
import logging


def check(
    scan_name: str, checks_path: str, data_source="staging", project_root="include"
):
    from soda.scan import Scan

    logging.info("Running Soda Scan ...")
    config_file = f"{project_root}/soda/configuration.yml"
    checks_base_path = f"{project_root}/soda/checks/tables"
    checks_path = os.path.join(checks_base_path, checks_path)
    logging.info(f"config_file={config_file}")
    logging.info(f"checks_path={checks_path}")
    logging.info(f"data_source={data_source}")

    scan = Scan()
    scan.set_verbose()
    scan.add_configuration_yaml_file(config_file)
    scan.set_data_source_name(data_source)
    scan.add_sodacl_yaml_files(checks_path)
    scan.set_scan_definition_name(scan_name)

    result = scan.execute()
    print(scan.get_logs_text())

    if result != 0:
        raise ValueError("Soda Scan failed")

    return result
