function pathadd
	if not contains $PATH $argv
		set PATH $argv $PATH
	end
end

set PROJECT_ROOT (dirname $argv[1])
set VIRTUAL_ENV_DIR $PROJECT_ROOT/venv

if not test -e $VIRTUAL_ENV_DIR
    python3.4 -m venv $VIRTUAL_ENV_DIR
    . $VIRTUAL_ENV_DIR/bin/activate.fish
    pip install -r requirements-dev.txt
end

if set -q $VIRTUAL_ENV
	. $VIRTUAL_ENV_DIR/bin/activate.fish
    set VIRTUAL_ENV rds-log-streamer
end
