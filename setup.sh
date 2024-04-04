echo "Please enter the repo URL!"
read URL
url="https://github.com/SamNour/TUMbot.git"
base_name=$(basename "$url" .git)
echo $base_name
git clone --bare $URL /home/bsp_projects/usr/git/$base_name.git
mkdir -p /home/bsp_projects/elixir-data/projects/$base_name/data
ln -s /home/bsp_projects/usr/git/$base_name.git /home/bsp_projects/elixir-data/projects/$base_name/repo
python3 /home/bsp_projects/elixir/update.py 12