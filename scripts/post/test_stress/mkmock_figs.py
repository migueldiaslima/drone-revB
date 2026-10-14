# extends the stress mock with a FREQ step (modes 1 to 12, analytic shapes) and RP node sets, for export_th_figs.py
import numpy as np, pickle
D=pickle.load(open('mock.pkl','rb'))
X=D['nodes']; n=len(X)
modes=[]
for k in range(13):
    u=np.c_[np.sin(0.2*k*X[:,0]), np.cos(0.1*k*X[:,1]), 0.01*k*X[:,2]]
    modes.append(u)
D['modes']=modes; D['freqs']=[0.0]*7+[431.0,432.5,437.2,441.4,457.2,533.4]
D['rp']={'RP_JNT_PP':[5],'RP_JNT_PM':[9]}
pickle.dump(D,open('mock.pkl','wb'))
