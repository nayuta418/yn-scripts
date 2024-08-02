#!/bin/bash
#A script to add this direcotry to ~/.bash_aliases or ~/.bash_profile

echo "Which OS are you using? Select number."
select os in "Linux" "MacOS" "quit"
do
  if [ "$REPLY" = "q" ] ; then
    echo "quit."
    exit 0
  fi
  if [ -z "$os" ] ; then
    continue
  elif [ $os == "Linux" ] ; then
    echo '' >> ~/.bash_aliases
    echo '#PATH for yn-scripts' >> ~/.bash_aliases
    echo "export PATH=\$PATH:$PWD" >> ~/.bash_aliases
    echo "PATH was added to ~/.bash_aliases"
    echo "Please close and re-run the terminal."

    break

  elif [ $os == "MacOS" ] ; then
    shell=$(echo $SHELL)
      if [ $shell == "/bin/bash" ]; then
        profile=~/.bash_profile
      elif [ $shell == "/bin/zsh" ]; then
        profile=~/.zprofile
      fi

    echo '' >> $profile
    echo '#PATH for yn-scripts' >> $profile
    echo "export PATH=\$PATH:$PWD" >> $profile
    echo "PATH was added to $profile"
    echo "Please close and re-run the terminal."

    break

  elif [ $os == "quit" ] ; then
     echo "quit."
     exit 0
  fi
done
