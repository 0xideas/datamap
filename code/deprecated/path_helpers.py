def all_files(path):
	# returns all files found on a mountpoint
	allfiles = [os.path.join(r, name) for r,d,f, in os.walk(path) for name in f]
	#changed splittext index from 1 to -1
	exts = [os.path.splitext(file)[-1].upper() for file in allfiles]
	df = pd.DataFrame([allfiles, exts]).T
	df.columns = ['filepath','ext']
	df['ext'] = df['ext'].astype('category')
	# df.ext.value_counts().nlargest(10)
	return df

def get_size(path = '.'):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp) if os.path.isfile(fp) else 0
	return total_size

def get_contents(path = '.'):
	files = []
	dirs = []
	for r, d, f in os.walk(path):
		files.append(f)
		dirs.append(d)

	return(dirs, files)