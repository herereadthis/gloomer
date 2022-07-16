read -p 'Username: ' uservar

# options to get password input
# read -sp 'Password: ' passvar

DEFAULT_LOG_FOLDER="~/adsb/logs/"

read -p 'word: ' word0
read -p 'word, again: ' word2
read -p "enter name of log folder (press enter to keep default ${DEFAULT_LOG_FOLDER}): " log_folder

# echo "Thank you ${uservar} `uservar`"
sentence="Hello ${uservar}, your password is ${passvar}"

echo -e "\n${sentence}\n"

if [[ "${word0}" == "${word2}" ]]; then
    echo "Strings are equal."
    # exit 0
else
    echo "Strings are not equal."
    # exit 1
fi

if [[ -z $log_folder ]]; then
  echo "Log Folder is ${DEFAULT_LOG_FOLDER}"
else
    echo "Log Folder is ${log_folder}"
fi




