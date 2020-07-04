Deployer
---
A very simple and small chatop for [pyslackops](https://github.com/jar349/pyslackops)
that can create deployments on GitHub repositories.

Sorry for the terrible name.

How I think this might work
---
before deploying:
 - mcops repo must be setup with a webhook to the deployer for deployment status events

slack user types: `.deploy https://github.com/jar349/mcops/pulls/2` 

pyslackops notices and routes to registered handler of .deploy: the deployer

deployer `/handle`s the .deploy command by:
 - creating a Deployment on the pull request

creating the Deployment kicks off a GitHub action that:
 - deploys mcops
 - creates a deployment status as its final act

deployer receives a webhook for the deployment status and matches it with the deployment it created
 - can now report status of the deployment back to slack user

 extra bonus: deploy history
 - deployer also serves a webapp that shows deploy history
