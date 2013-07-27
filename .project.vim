let g:cmd="w | !jekyll build && open http://localhost:4000/writings/" . fnamemodify(bufname("%"), ":t:r:s?^[0-9]*-[0-9]*-[0-9]*-??") . "/"
