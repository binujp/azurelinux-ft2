// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package interfaceutils

import (
	"fmt"
)

// user should not have to care if it is a toolchain package or non toolchain package
func BuildToolchain() (err error) {
	fmt.Println("Building toolchain ...")
	// check if we need to build toolchain
	var shouldBuild bool
	shouldBuild, err = buildStatusToolchain()
	if shouldBuild {
		err = buildToolchainHere()
		if err != nil {
			err = fmt.Errorf("failed to build toolchain:\n%w", err)
			return err
		}
	}
	return
}

func buildToolchainHere()(err error) {
	return
}

