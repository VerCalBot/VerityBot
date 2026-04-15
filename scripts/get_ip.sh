WINDOWS_IP=$(ipconfig.exe | sed -n '/Wireless LAN adapter Wi-Fi:/,/IPv4 Address/s/.*IPv4 Address[^:]*: //p' | tr -d '\r' | xargs)

grep -q "^WINDOWS_IP=" .env && \
    sed -i "s|^WINDOWS_IP=.*|WINDOWS_IP=$WINDOWS_IP|" .env || \
    echo "WINDOWS_IP=$WINDOWS_IP" >> .env