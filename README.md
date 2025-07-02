# aws-boto3-mcp-private

[certified by MCP Review](https://mcphub.com/mcp-servers/didier-durand/aws-boto3-mcp-private)

AWS Boto3 (Python) MCP Server is a MCP server aimed at executing Python code using the Boto3 client from the AWS Python 
SDK implemented to monitor and manage AWS resources in a given account. 

The security is ensured by the fact that the MCP client (i.e a Large Language Model (LLM), an AI agent, a developer tool 
like AWS Q Developer or Claude Desktop, etc.) has to provide the proper AWS credentials (access key and secret key) as 
input parameters to the code executor supplied as a MCP tool by this MCP server.

The architecture is the following:
* a front-end MCP server implemented as required by the official MCP architecture
* a backend Docker container on AWS LightSail, managed service to easily run containers on AWS Cloud.

Restrict access https://docs.aws.amazon.com/en_us/lightsail/latest/userguide/amazon-lightsail-editing-firewall-rules.html

The MCP specs have been updated on March 25th, 2025 to include OAuth2 security: https://auth0.com/blog/an-introduction-to-mcp-and-authorization/
