set fish_greeting
function fish_prompt
    set_color blue
    echo -n "｢ ｣" #  # # 
    printf "   "
    set_color cyan
    echo -n "｢ "(prompt_pwd)" ｣"
    set_color normal
end
fastfetch
##--------------------------------------------##

# Created by `pipx` on 2024-06-09 20:26:40
set PATH $PATH /home/hivo/.local/bin

fish_add_path /home/hivo/.spicetify

set -x SPOTIPY_CLIENT_ID '6bf8c4d08295475b9dc1f76844cd50ad'
set -x SPOTIPY_CLIENT_SECRET '0c04dd8a15334550bb40897e7362e3c5'
set -x SPOTIPY_REDIRECT_URI 'http://localhost:8888/callback'

##--------------------------------------------##
alias la='ls -a'
##--------------------------------------------##
function z
    if test (count $argv) -eq 0
        echo "Usage: z <file>"
        return 1
    end

    set file $argv[1]
    set extension (string match -r '.*\.([^.]+)$' $file)[2]

    switch $extension
        case 'tar.gz' 'tgz'
            tar xzf $file
        case 'tar.bz2' 'tbz'
            tar xjf $file
        case 'tar.xz'
            tar xJf $file
        case 'tar'
            tar xf $file
        case 'gz'
            gunzip $file
        case 'bz2'
            bunzip2 $file
        case 'xz'
            unxz $file
        case 'zip'
            unzip $file
        case '*'
            echo "Unsupported file type"
            return 1
    end
end
