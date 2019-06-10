source ./container.properties
# -------->>>>>>>>Bulk delete start <<<<<<<<<<-----------
# 1. Export Token
export token=$(curl -v -X GET -H "X-Storage-User: $user" -H "X-Storage-Pass: $password" $serverauth  2>&1 | grep X-Auth-Token | sed 's/< X-Auth-Token: //')
echo token=$token

for container in $containers
do
    # 2. List all objects
    curl -v -X GET -H "X-Auth-Token: $token" $server/$container > $container

    # 3. Add container name
    sed -i "s|^|$container/|g" ./$container
    
    # 4. Bulk delete
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Deleting container $container"
    curl -v -X DELETE -H "X-Auth-Token: $token" -H "Content-Type: text/plain" -T ./$container $server?bulk-delete
done
# -------->>>>>>>>Bulk delete end <<<<<<<<<<-----------