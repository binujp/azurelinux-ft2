// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package interfaceutils

import (
	"os/exec"
	"fmt"

//	packagelist "github.com/microsoft/azurelinux/toolkit/tools/internal/packlist"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/specreaderutils"
)

var (
	azlSpecsDirs = [...] string {"SPECS", "SPECS-EXTENDED", "SPECS-SIGNED"}
)

func BuildPackage(spec string) (err error) {

	fmt.Println("Building packages specs are (%s)", spec)

	// check specs exist
	specsDir, err := validateSpecExistance(spec)
	if err != nil {
		err = fmt.Errorf("failed to validate specs:\n%w", err)
		return err
	}

	// any other checks

	// build toolchain if required

	// put toolchain rpms into toolchain_archive and use it

	// build tools if required

	// set extra configs

	// show dependency graph - use graphanalytics tool

	// build package
	err = buildSpecs(spec, specsDir)
	if err != nil {
		err = fmt.Errorf("failed to build specs:\n%w", err)
		return err
	}

	// show output

	return
}

// validateSpecExistance checks if each spec in specList exists
// and assigns it the correct specsDir in which it exists
func validateSpecExistance(specList string) (specsDir string, err error) {
	fmt.Println("Checking if spec exists for (%s)", specList)
//	specMap, err := packagelist.ParsePackageList(*specList)
//	if err != nil {
//		err = fmt.Errorf("failed to parse package list file:\n%w", err)
//		return nil, err
//	}
	
	// TODO: currently, we have a limitation that all specs to be built must be present in the same specsDir
	var specMap = make(map[string]bool)
	for _, specsDir := range azlSpecsDirs {
		specFiles, err := specreaderutils.FindSpecFiles(specsDir, specMap)
		if err != nil {
			err = fmt.Errorf("failed to FindSpecFiles:\n%w", err)
			return "", err
		} else {
			fmt.Println("done with specreader, returned specFiles (%s)", specFiles)
			return specsDir, nil
		}
	}	
	fmt.Println("done with specreader")
	return
}

func execCommands(app, dir string, args []string) (stdoutStr string, err error) {
	cmd := exec.Command(app, args...)
	if dir != "" {
		cmd.Dir = dir
	}
	stdout, err := cmd.CombinedOutput()
	return string(stdout), err
}

func buildSpecs(specs, specsDir string) (err error) {
	fmt.Println("exuting using new funtion")
	args := []string{"build-packages", "SRPM_PACK_LIST=\"cracklib\"", "SPECS_DIR=/home/neha/repos/test/CBL-Mariner/SPECS2/"}
	stdout, err := execCommands("/usr/bin/make", "/home/neha/repos/test/CBL-Mariner/toolkit/", args)
	fmt.Println(stdout)
	fmt.Println(err)
	return
}

func buildSpecs2(specs, specsDir string) (err error) {
		app := "ls"
	cmd := exec.Command(app)
	stdout, err := cmd.Output()

    if err != nil {
        fmt.Println(err.Error())
        return
    }

    fmt.Println(string(stdout))

	app = "make"

	cmd = exec.Command(app, "check-x86_64-manifests")
	cmd = exec.Command(app, "check-aarch64-manifests")
	cmd.Dir = "/home/neha/repos/test/CBL-Mariner/toolkit/"
	stdout, err = cmd.Output()

	fmt.Println("output is", string(stdout))

    if err != nil {
        fmt.Println("error is",err)
        return
    }

    // Print the output
    fmt.Println(string(stdout))
	
	cmd = exec.Command(app, "package-toolkit")
	cmd = exec.Command(app, "toolchain", "REBUILD_TOOLCHAIN=n", "DAILY_BUILD_ID=3-0-20240321")
	cmd = exec.Command(app, "build-packages", "SRPM_PACK_LIST=\"cracklib\"", "SPECS_DIR=/home/neha/repos/test/CBL-Mariner/SPECS2/")
	cmd.Dir = "/home/neha/repos/test/CBL-Mariner/toolkit/"
	stdout, err = cmd.CombinedOutput()
    fmt.Println("output is", string(stdout))

    if err != nil {
        fmt.Println("error is",err)
        return
    }

    // Print the output
    fmt.Println(string(stdout))

	return
}
