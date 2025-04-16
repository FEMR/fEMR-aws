import React, { useState, useEffect } from "react";
import Button from "@mui/material/Button";

function FemrInstallationGuide() {
  const [intelMacLink, setIntelMacLink] = useState("");
  const [armMacLink, setArmMacLink] = useState("");
  const [architecture, setArchitecture] = useState(null);

  const getDownloadLinks = async () => {
    try {
      const intelMacResponse = await fetch(
        `https://qetcdnt6vd.execute-api.us-east-2.amazonaws.com/prod/installer/macos/intel`
      );
      const intelLink = await intelMacResponse.text();

      setIntelMacLink(intelLink);
      const armMacResponse = await fetch(
        `https://qetcdnt6vd.execute-api.us-east-2.amazonaws.com/prod/installer/macos/arm`
      );
      const armLink = await armMacResponse.text();

      setArmMacLink(armLink);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const fetchArch = async () => {
      if (navigator.userAgentData) {
        try {
          const result = await getArchitecture();
          const arch = result.architecture.toLowerCase();
          if (arch.includes("arm")) {
            setArchitecture("arm");
          } else if (arch.includes("x86")) {
            setArchitecture("intel");
          } else {
            console.warn("Unknown architecture:", arch);
            setArchitecture(null);
          }
          console.log("Architecture:", arch); // e.g., arm or intel
        } catch (error) {
          console.error("Error fetching architecture:", error);
          setArchitecture(null);
        }
      } else {
        console.log("navigator.userAgentData is not available");
      }
    };

    fetchArch();
  }, []);

  useEffect(() => {
    if (architecture) {
      getDownloadLinks();
    } else {
      console.log("Architecture is not set, providing customer choice.");
    }
  }, [architecture]);

  const getArchitecture = async () => {
    const arch = await navigator.userAgentData.getHighEntropyValues([
      "architecture",
    ]);
    return arch;
  };

  const handleDownload = (arch) => {
    if (arch === "arm") {
      window.open(armMacLink);
    }
    if (arch === "intel") {
      window.open(intelMacLink);
    }
  };

  return (
    <html>
      <body>
        <div>
          <center>
            <img src="../logo_color.png" alt="FEMR Logo" />
          </center>
        </div>
        <div>
          <center>
            <h1> How to Install Femr On MacOSX </h1>
          </center>
          <center>
            <p>
              {" "}
              <b>&nbsp;&nbsp;1. Download and Install Docker</b>{" "}
            </p>
          </center>
          <center>
            <pre>
              &nbsp;&nbsp;&nbsp;&nbsp;Docker is a tool that the Femr service
              uses and must be installed and running during<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;any step of this process and while the
              FEMR system is being used.<br></br>
              <br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;Go to&nbsp;
              <a
                href="https://www.docker.com/products/docker-desktop/"
                target="_blank"
              >
                https://www.docker.com/products/docker-desktop/
              </a>{" "}
              and download the release for your computer.<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;Open the downloaded dmg and drag the
              Docker application the Applications folder.
              <br></br>
            </pre>
          </center>
          <center>
            <p>
              {" "}
              <b>&nbsp;&nbsp;2. Download the FEMR installer</b>{" "}
            </p>
          </center>
          <center>
            {architecture ? (
              <div class="macButton">
                <Button
                  variant="contained"
                  disabled={
                    architecture === "intel"
                      ? intelMacLink === ""
                      : armMacLink === ""
                  }
                  onClick={() => handleDownload(architecture)}
                  color="primary"
                  textTransform="none"
                >
                  Install fEMR
                </Button>
              </div>
            ) : (
              <>
                <div class="macButton">
                  <Button
                    variant="contained"
                    disabled={intelMacLink === ""}
                    onClick={() => handleDownload("intel")}
                    color="primary"
                    textTransform="none"
                  >
                    Install fEMR (Intel Mac)
                  </Button>
                </div>
                <div class="macButton">
                  <Button
                    variant="contained"
                    disabled={armMacLink === ""}
                    onClick={() => handleDownload("arm")}
                    color="primary"
                    textTransform="none"
                  >
                    Install fEMR (Arm Mac)
                  </Button>
                </div>
              </>
            )}
          </center>
          <center>
            <p>
              {" "}
              <b>&nbsp;&nbsp;3. Open Docker</b>{" "}
            </p>
          </center>
          <center>
            <pre>
              &nbsp;&nbsp;&nbsp;&nbsp;Open the Docker app that you previously
              installer and accept the terms and
              <br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;conditions. The Docker dashboard should
              look something like this:<br></br>
              <br></br>
            </pre>
          </center>
          <center>
            <img
              src="../Docker_example.png"
              alt="Docker Dashboard"
              width="750"
              height="375"
            />
          </center>
          <center>
            <p>
              {" "}
              <b>&nbsp;&nbsp;4. Launch the FEMR Installer Package</b>{" "}
            </p>
          </center>
          <center>
            <pre>
              &nbsp;&nbsp;&nbsp;&nbsp;Make sure Docker is still running and
              double click the FEMR installer, accept the license<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;and click through the steps. Eventually
              you will be prompted to login with your
              <br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;credentials you obtained through the
              off-chain enrollment process.<br></br>
            </pre>
          </center>
          <center>
            <p>
              {" "}
              <b>&nbsp;&nbsp;5. Launch the FEMR service</b>{" "}
            </p>
          </center>
          <center>
            <pre>
              &nbsp;&nbsp;&nbsp;&nbsp;Go to your applications folder and double
              click the FEMR executable. This will launch a<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;terminal window. The first time you run
              this please make sure you are connected to<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;the internet the first time and be patient
              this first run may take up to 30 minutes (after<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;first run, the program may be used offline
              and will be launched in less than a minute)<br></br>
            </pre>
          </center>
          <center>
            <p>
              {" "}
              <b>&nbsp;&nbsp;6. Navigate to the FEMR page</b>{" "}
            </p>
          </center>
          <center>
            <pre>
              &nbsp;&nbsp;&nbsp;&nbsp;Open a browser window and navigate to{" "}
              <a href="https://localhost:9000" target="_blank">
                https://localhost:9000
              </a>{" "}
              if you see the FEMR<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;login page, success!
              <br></br>
            </pre>
          </center>
        </div>
      </body>
    </html>
  );
}

export default FemrInstallationGuide;
