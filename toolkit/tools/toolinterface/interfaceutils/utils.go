// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package interfaceutils

import (
	"fmt"
)

// buildStatus checks if spec needs to be rebuilt
// reasons for rebuild:
//					- spec has never been built
//					- there is a change in spec from last build
//					- there is a change in toolchain manifest
//					- user wants to rebuild spec
func buildStatus() (err error) {
	fmt.Println("in buildStatus")
	return

}

// buildStatusToolchain checks if toolchain should be (re)built
// returns true if
//					- toolchain rpms have never been built
//					- there is a change in toolchain spec(s)
//					- there is a change in toolchain manifest
//					- user wants to rebuild toolchain
func buildStatusToolchain() (rebuildOpt bool, err error) {
	err = buildStatus()
	// added if change in manifest files
	return false, nil
}
