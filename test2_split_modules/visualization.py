def drawHeatmap(df,annot): # heatmap
    fig, axs = plt.subplots()
    sns.heatmap(df, annot=False, linewidths=1, cmap=plt.cm.viridis.reversed(),
                vmin=df.min().min(), vmax=df.max().max(),
               xticklabels=range(-6,9,3), yticklabels=df.index, cbar_kws={'label':'Thickness [nm]'})
    axs.set(title='Surface uniformity', xlabel='X [cm]', ylabel='Y [cm]')
    fig.savefig(f'data/{today}/2d_{annot}.png')
    
def polygon_under_graph(x, z):
    return [(x[0], 0.), *zip(x, z), (x[-1], 0.)]
    
def draw3DPlot(df,annot):
    fig = plt.figure(figsize=(8,8))
    axs = fig.add_subplot(projection='3d')
    
    df = df.astype(float)
    x = range(-6,9,3) # fixed
    y = df.index.tolist()
    z = df.values.tolist()
    
    verts = [polygon_under_graph(x, z[i]) for i in range(len(y))]
    facefolors = ['yellow' if (val < 5.5) | (val > 15.5) else 'gray' for val in y]
    poly = PolyCollection(verts, facecolor=facefolors, edgecolor='black', alpha=.7)
    axs.add_collection3d(poly, zs=y, zdir='y')
    axs.set(xlim=(-6, 6), ylim=(y[0], y[-1]), zlim=(min(min(z)), max(max(z))),
           xlabel='X [cm]', ylabel='Y [cm]', zlabel='Thickness [nm]')
    axs.set_title('Surface uniformity', y=1)
    axs.set_box_aspect(None, zoom=0.8)
    axs.view_init(40, 45) 
    fig.savefig(f'data/{today}/3d_{annot}.png')
