# Step 1: Get Your Azure OpenAI Details From Microsoft Foundry

In this exercise, you collect the Azure OpenAI connection details from Microsoft
Foundry so the agent can call the deployed chat model. This matters because every
later step depends on the same endpoint, API key, and deployment name being
available in the existing **.env** file.


## Log in to Microsoft Foundry

1. Open the Edge browser.
2. Navigate to **https://ai.azure.com** in the browser's address bar, if it's not already open.
3. Click **Sign in** in the top-right corner.
4. Sign in with the details below:    
    **Username**: +++@lab.CloudPortalCredential(User1).Username+++    
    **Password (TAP)**:  +++@lab.CloudPortalCredential(User1).AccessToken+++     
5. In the top bar, toggle on the **New Foundry** switch.
6. From the project dropdown, select the only project available and click **Let's go**.
7. When the **Welcome to the new Microsoft Foundry** box appears, click **X** in the top-right corner.

After you close the welcome box, you should see the Microsoft Foundry home page
with **API key**, **Project endpoint**, and **Azure OpenAI endpoint** boxes near
the top of the page.

1. Copy the value from the **Azure OpenAI endpoint** box. If the copied endpoint
    ends with **/openai/v1**, remove that part before adding it to
    **.env**. For example, change
    **https://foundry-12345.openai.azure.com/openai/v1** to
    **https://foundry-12345.openai.azure.com**.
2. Copy the value from the **API key** box.
3. Open the existing **.env** file in VS Code.
4. Add or update the endpoint and API key in **.env**.
5. In the top navigation, select **Build**.
6. Open **Models**.
7. Confirm that **gpt-5.5** and **gpt-4.1-mini** are listed and each one has a **Succeeded** status.
8. Confirm that **AZURE_OPENAI_DEPLOYMENT_NAME** in **.env** matches **gpt-5.5**.
9. Confirm that **CITY_GUIDE_AZURE_OPENAI_DEPLOYMENT_NAME** in **.env** matches **gpt-4.1-mini**.

Your **.env** file should include these values:

```env
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<your-azure-openai-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.5
CITY_GUIDE_AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini
```

## What You Learned

You found the Azure OpenAI endpoint, API key, and deployment name in Microsoft
Foundry and added them to the agent configuration.
