ssh -i ./pbl_ssh_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null pbl@$(ip neigh | grep enx | cut -f 1 -d " ")
