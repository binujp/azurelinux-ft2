// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package interfaceutils

import (
	"fmt"
	"os/exec"
)

// ReadyChanges runs various tools to ready changes for contributing to upstream open source repo
// TODO: use a command builder
func ReadyChanges() (err error) {
	fmt.Println("Ready changes ...")
	
	// see if there are any changes in spec licenses, and update licenses.json file
	c := exec.Command("toolkit/scripts/license_map.py")

	if err := c.Run(); err != nil {
		err = fmt.Errorf("failed to run license_map.py:\n%w", err)
	}

	// see if there are any changes in toolchain specs, and update manifest files
	var arch = "x86_64"
	c = exec.Command("source toolkit/scripts/toolchain/check_manifests.sh -a $arch")

	if err := c.Run(); err != nil {
		err = fmt.Errorf("failed to run check_manifests.sh for arch (%s):\n%w", arch, err)
	}

	arch = "aarch64"
	c = exec.Command("source toolkit/scripts/toolchain/check_manifests.sh")

	if err := c.Run(); err != nil {
		err = fmt.Errorf("failed to run check_manifests.sh for arch (%s):\n%w", arch, err)
	}
	return
}
