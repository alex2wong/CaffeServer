from matplotlib import pyplot as plt
import json

im = plt.imread("./assets/test7.png")
ax = plt.subplot(111)

plt.imshow(im)

f = open("./assets/test7.jpg.txt", 'r')
content = f.read()
print(content)

JSONobjs = json.loads(content)
print "read content: " + content

objs = JSONobjs["objects"]
print "objs num: " + str(len(objs))
for obj in objs:
    print obj
    if "obj" not in obj:
        continue
    bbox = obj["obj"]
    class_name = obj["class"]
    score = obj["score"]
    print "got info: " + class_name
    ax.add_patch(
        plt.Rectangle((bbox[0], bbox[1]),
                         bbox[2] - bbox[0],
                         bbox[3] - bbox[1], fill=False,
                         edgecolor='red', linewidth=3.5)
           )
    ax.text(bbox[0], bbox[1] - 2,
           '{:s} {:.3f}'.format(class_name, score),
           bbox=dict(facecolor='blue', alpha=0.5),
           fontsize=14, color='white')

# plt.axis('off')
plt.tight_layout()
# plt.draw()
plt.show()
