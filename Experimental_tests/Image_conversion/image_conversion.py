import multiprocessing as mp
import subprocess
import sys

image_array = []


def test(image):
    # convert
    full_uri = "myregistry.domain.com/"+image+":latest"
    ter = "time /root/dadi/bin/ctr obdconv " + full_uri + " " + full_uri + "_obd_new"
    output = subprocess.getoutput(ter)
    lock.acquire()
    tf = open(sys.argv[2], "a")
    print(image)
    # print(output)
    print(image,file=tf)
    print(output,file=tf)
    tf.close()
    lock.release()

def init_lock(l):
    global lock
    lock = l


if __name__ == '__main__':

    f = open("/root/images/images_to_analysis", "r")
    lines = f.readlines()
    for line in lines:
        a = line.rstrip()
        image_array.append(a)

    extra_image = image_array * 2
    image_array = image_array + extra_image

    l = mp.Lock()
    p = mp.Pool(processes=int(sys.argv[1]), initializer=init_lock, initargs=(l,))

    for item in image_array:
        p.apply_async(test, (item,))

    p.close()
    p.join()
