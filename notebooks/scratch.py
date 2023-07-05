import matplotlib.pyplot as plt
filepath = "../docs/imgs/cellsite.jpeg"
img_cellsite = plt.imread(filepath)
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.imshow(img_cellsite);