import os

import hvac


def get_required_env_var(name):
    value = os.getenv(name)
    if not value:
        raise EnvironmentError("You need to provide the environment variable{}".format(name))

    return value


def get_vault_client():
    app_role_id = get_required_env_var('APP_ROLE_ID')
    app_secret_id = get_required_env_var('APP_SECRET_ID')
    vault_addr = get_required_env_var('VAULT_ADDR')

    client = hvac.Client(url=vault_addr)
    client.auth_approle(app_role_id, app_secret_id)

    return client


def get_database_credentials(vault_client: hvac.Client) -> (str, str):
    database_credential_endpoint = get_required_env_var('APP_DB_ROLE')
    db_credentials = vault_client.secrets.database.generate_credentials(name=database_credential_endpoint).pop('data')

    user = db_credentials.pop('username')
    password = db_credentials.pop('password')

    return user, password


def get_static_credentials(vault_client: hvac.Client) -> dict:
    static_secret_path = get_required_env_var('STATIC_SECRET_PATH')
    static_credentials = vault_client.secrets.kv.v2.read_secret_version(mount_point='kv',
                                                                        path=static_secret_path).pop('data').pop('data')

    return {key: static_credentials[key] for key in static_credentials.keys()}
