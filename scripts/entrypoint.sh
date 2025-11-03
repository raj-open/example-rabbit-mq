#!/usr/bin/env bash
# ----------------------------------------------------------------
# Entry point for main application
# ----------------------------------------------------------------

set -e

cd //home/basicuser/app

echo "[entrypoint] Correct permissions for mounted volumes"
[ -d "logs" ] && chown -R basicuser:basicgroup "logs"
[ -d "data" ] && chown -R basicuser:basicgroup "data"
echo "[entrypoint] complete."

# switch to user
# preserve environment (variables)
# start bash session
sudo \
    -u "basicuser" \
    --preserve-env \
    bash -c "
        # preserve environment (secrets)
        source /run/secrets/credentials
        # run command
        $*
    "
