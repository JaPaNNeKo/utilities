import yggdrasil as ygg
# ygg.create(["tool_local","tool_git"])
# ygg.remove() # todo debug if nothing
ygg.create("tool_git", force_regen=True, debug=True)
