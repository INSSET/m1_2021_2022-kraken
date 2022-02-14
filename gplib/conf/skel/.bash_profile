trap "{ logout; }" SIGINT
/usr/bin/ssh {USER}@{IP}
logout