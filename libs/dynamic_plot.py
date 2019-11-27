import os,sys
import psse34
import dyntools
import matplotlib.pyplot as plt
import pandas as pd
import glob

def dynamic_plot_custom(output_file):
	outfile = dyntools.CHNF(output_file)
	short_title, chid_dict, chandata_dict = outfile.get_data()
	df_chan = pd.DataFrame(chandata_dict)
	df_chan.rename(columns=chid_dict, inplace=True)
	df_chan.to_csv('{}.csv'.format(output_file))

# plot results
def psse_plot(df, csv_file, title):
	for i in df.columns:
		df.loc[:, [i]].plot()
		plt.title(title)
		plt.savefig('{}_{}.png'.format(csv_file.split(".")[0], i))	
	return

def df_read(csv):
	df = pd.read_csv(csv)
	df['Time(s)'] = df['Time(s)'].astype(float)
	df = df.set_index('Time(s)')
	return df

# def select_v(df, s, t, u, f):
# 	col_v = [j for j in df.columns if j.startswith(s)]
# 	print(col_v)
# 	if len(col_v)>0:
# 		df_ = df.loc[:, col_v]
# 		# print(df_)
# 		title_s = t
# 		df_.plot()
# 		plt.title(t)
# 		plt.ylabel(t + " " + u)
# 		plt.legend(fontsize=10)
# 		plt.savefig('plt\\{}_{}.png'.format(f.split("\\")[1][:-8], title_s))
# 		plt.close()
# 	else:
# 		print('No variables about {0} defined in the output file {1}'.format(s[0], f))

def select_v(df, s, t, u, f, proj):
	col_v = [j for j in df.columns if j in s]
	print(col_v)
	if len(col_v)>0:
		df_ = df.loc[:, col_v]
		# print(df_)
		title_s = t
		df_.plot()
		ymin, ymax = plt.ylim()
		if abs(ymax-ymin) < 0.01:
			yminnew = ymin-0.1
			ymaxnew = ymax+0.1
		else:
			yminnew = ymin-0.1*abs(ymax-ymin)
			ymaxnew = ymax+0.1*abs(ymax-ymin)
		plt.ylim(yminnew, ymaxnew)
		plt.title(t)
		plt.ylabel(t + " " + u)
		plt.legend(fontsize=10)
		plt.savefig('plt\\{0}\\{1}_{2}.png'.format(proj, f.split("\\")[-1][:-8], title_s))
		#plt.savefig('plt\\{1}_{2}.png'.format(f.split("\\")[-1][:-8], title_s))
		plt.close()
	else:
		print('No variables about {0} defined in the output file {1}'.format(s[0], f))

def pplot(csv_files, v_plot, proj=None):
	df = pd.DataFrame()
	dirs = os.listdir(os.getcwd())
	if 'plt' not in dirs:
		os.mkdir('plt')
	if not os.path.isdir('plt\\{}'.format(proj)):
		os.mkdir('plt\\{}'.format(proj))

	for i, f in enumerate(csv_files):
		print(f)
		df = df_read(f)
		# print(df)
		flg = 0
		if flg:
			select_v(df, 'V_', 'Voltage Profile', '(p.u.)', f)		
			select_v(df, 'P_', 'Active Power Profile', '(MW)', f)
			select_v(df, 'Q_', 'Reactive Power Profile', '(MVar)', f)
			select_v(df, 'F_', 'Frequency Profile', '(Hz)', f)
		else:
			for k in v_plot:
				select_v(df, v_plot[k][0], k, v_plot[k][1], f, proj)	
			# select_v(df, ['P_PASF', 'Q_PASF'], , '(MW/MVAR)', f)
			# select_v(df, ['V_PCC_PASF'], 'Inverter Power Profile', '(MW/MVAR)', f)
			# select_v(df, ['V_PCC_PASF'], 'Inverter Power Profile', '(MW/MVAR)', f)
		# raise