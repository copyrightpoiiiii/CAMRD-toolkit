package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"syscall"
	"time"

	"github.com/containerd/containerd"
	"github.com/containerd/containerd/cio"
	"github.com/containerd/containerd/namespaces"
	"github.com/containerd/containerd/oci"
	"github.com/containerd/containerd/snapshots"
)

var image_name = flag.String("name", "", "")
var image_tag = flag.String("tag", "", "")
var out_path = flag.String("out", "", "")

func main() {

	flag.Parse()

	client, err := containerd.New("/run/containerd/containerd.sock")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer client.Close()

	ctx := namespaces.WithNamespace(context.Background(), "default")
	file, err := os.OpenFile(*out_path, os.O_CREATE|os.O_APPEND|os.O_RDWR, os.ModeAppend)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer file.Close()

	snps := client.SnapshotService("overlaybd")
	snps.Remove(ctx, "test")

	st := map[string]string{}

	fmt.Fprintf(file, *image_name+":"+*image_tag+"\n")
	ref := *image_name + ":" + *image_tag
	fmt.Println(ref)

	// rpull image
	cmd := "/root/dadi/bin/ctr rpull " +
		*image_name + ":" + *image_tag
	cmd_out, err := bash(cmd)
	if err != nil {
		fmt.Fprintf(file, "skip: bash: %s\n", cmd_out)
		return
	}

	fmt.Fprintf(file, "%s\n", cmd_out)

	i, err := client.ImageService().Get(ctx, ref)
	if err != nil {
		fmt.Println("get image:", err)
		return
	}
	var image containerd.Image
	image = containerd.NewImage(client, i)
	unpacked, err := image.IsUnpacked(ctx, "overlaybd")
	if err != nil {
		fmt.Println("check unpack:", err)
		return
	}

	if !unpacked {
		if err := image.Unpack(ctx, "overlaybd"); err != nil {
			fmt.Println("unpack:", err)
			return
		}
		fmt.Println("unpacked")
	}
	fmt.Println("start",*image_name+":"+*image_tag)
	startTime := time.Now()
	container, err := client.NewContainer(
		ctx,
		"test",
		containerd.WithImage(image),
		containerd.WithSnapshotter("overlaybd"),
		containerd.WithNewSnapshot("test", image, snapshots.WithLabels(st)),
		containerd.WithNewSpec(oci.WithImageConfig(image)),
	)
	if err != nil {
		fmt.Println("new container:", err)
		return
	}
	defer container.Delete(ctx, containerd.WithSnapshotCleanup)
	elapsedTime := time.Since(startTime) / time.Millisecond
	fmt.Fprintf(file, "%d ", elapsedTime)

	startTime = time.Now()
	task, err := container.NewTask(ctx, cio.NewCreator(cio.WithStdio))
	if err != nil {
		fmt.Println("new task:", err)
		return
	}
	defer task.Delete(ctx)
	elapsedTime = time.Since(startTime) / time.Millisecond
	fmt.Fprintf(file, "%d ", elapsedTime)

	task.Wait(ctx)

	startTime = time.Now()
	if err := task.Start(ctx); err != nil {
		fmt.Println("start task:", err)
		return
	}
	elapsedTime = time.Since(startTime) / time.Millisecond
	fmt.Fprintf(file, "%d \n", elapsedTime)

	if err := task.Kill(ctx, syscall.SIGTERM); err != nil {
		fmt.Println(err)
		return
	}

	task.Delete(ctx, containerd.WithProcessKill)
	return
}


func bash(cmd string) (string, error) {
	c := exec.Command("bash", "-c", cmd)
	output, err := c.CombinedOutput()
	if err != nil {
		c = exec.Command("bash", "-c", "/root/download/dadi/rm.sh")
		c.CombinedOutput()
		c = exec.Command("bash", "-c", cmd)
		output, err = c.CombinedOutput()
	}
	return string(output), err
}