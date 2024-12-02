import docker
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate username combinations and run Sherlock on a remote Docker host.")
    parser.add_argument("name", type=str, help="The name to generate username combinations from.")
    args = parser.parse_args()

    # Extract name from arguments
    name = args.name
    combinations = [
        name.replace(" ", "_").lower(),
        name.replace(" ", ".").lower(),
        name.replace(" ", "").lower(),
        f"{name.split()[0]}{name.split()[1]}".lower(),
        f"{name.split()[1]}_{name.split()[0]}".lower(),
        f"{name.split()[0]}_{name.split()[1]}123".lower(),
        f"{name.split()[0][0]}_{name.split()[1]}".lower(),
        f"{name.split()[0]}_{name.split()[1][0]}".lower(),
    ]

    # Connect to the remote Docker host
    docker_host = "tcp://localhost:2375"  # Replace <remote-docker-ip> with the Docker host IP
    client = docker.DockerClient(base_url=docker_host)

    # Run Sherlock for each username
    for username in combinations:
        print(f"Running Sherlock for username: {username}")
        try:
            # Run the Docker container
            result = client.containers.run(
                "sherlock/sherlock",                 # Docker image
                f"{username} --json /output/results.json",  # Command
                remove=True,                        # Automatically remove the container
                volumes={
                     "/var/sherlock_results": {"bind": "/output", "mode": "rw"}
                }
            )
            print(f"Results for {username}: {result.decode()}")
        except docker.errors.ContainerError as e:
            print(f"Error running Sherlock for {username}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error for {username}: {e}")

if __name__ == "__main__":
    main()
