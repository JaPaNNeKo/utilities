import yggdrasil as ygg
# ygg.create(["tool_local","tool_git"])
mger = ygg.AppManager.from_default()
print(mger.apps)
import pdb;pdb.set_trace()
# ygg.create("tool_git", force_regen=True, debug=True)
