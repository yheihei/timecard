#!/bin/sh

# TEST DB
if [ "$MYSQL_SECONDARY_DATABASE" ]; then
    echo 'Create secondary database...'
    echo "CREATE DATABASE IF NOT EXISTS \`$MYSQL_SECONDARY_DATABASE\` ;" | "${mysql[@]}"
    echo "GRANT ALL ON \`$MYSQL_SECONDARY_DATABASE\`.* TO 'root'@'%' ;" | "${mysql[@]}"
    echo 'FLUSH PRIVILEGES ;' | "${mysql[@]}"
fi
