# Step 1: Get Your Azure OpenAI Details From Microsoft Foundry

Start by collecting the Azure OpenAI values the agent needs to call the model.
Open Microsoft Foundry, select your project, and find the deployed chat model you
will use for the main agent.


## Log in to Microsoft Foundry

1. Open the browser. On the lab VM, this will be the Edge browser in the bottom taskbar.
2. Navigate to `https://ai.azure.com` in the browser's address bar, if it's not already open.
3. Sign in with the details below:    
    **Username**: +++@lab.CloudPortalCredential(User1).Username+++    
    **Password (TAP)**:  +++@lab.CloudPortalCredential(User1).AccessToken+++     
4. In the top bar, toggle on the **New Foundry** switch.
5. From the project dropdown, select the only project available and click **Let's go**.



1. Open the Microsoft Foundry portal.
2. Select your project.
3. Open **Models + endpoints**.
4. Select the chat model deployment for the workshop.
5. Copy the endpoint, API key, and deployment name into the existing `.env` file.

> Screenshot placeholder: Microsoft Foundry project page with **Models +
> endpoints** highlighted.

> Screenshot placeholder: model deployment details showing the deployment name.

> Screenshot placeholder: endpoint and key location for the Azure OpenAI
> resource.

Add these values to `.env`:

```env
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<your-azure-openai-key>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-main-agent-deployment>
```

## What You Learned

You found the Azure OpenAI endpoint, API key, and deployment name in Microsoft
Foundry and added them to the agent configuration.
