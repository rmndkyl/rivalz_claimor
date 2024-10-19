# Setting up Rivalz Fragment Auto-Claim
### Update packages
<code>apt-get update -y; apt upgrade -y</code>
### Install the screen utility
<code>sudo apt-get install screen</code>
### Open a screen session
<code>screen -S rivalz_auto_claim</code>
### Clone the script
<code>git clone https://github.com/rmndkyl/rivalz_claimor.git</code>
### Navigate to the script folder
<code>cd rivalz_claimor</code>
### Download and install Python
<code>add-apt-repository -y ppa:deadsnakes/ppa</code></br>
<code>apt-get install python3.12 -y</code></br>
<code>apt install python3-pip -y</code></br>
### Install dependencies
<code>pip install -r requirements.txt</code>
### Run the script
<code>python app.py</code></br>
![image](https://github.com/user-attachments/assets/ddafc498-05f5-47ab-a4a0-804587ff2f65)


# What it does::
1. Claims to your wallet (you will need to enter your seed phrase or privatekey)</br>
2. Claims to a newly created wallet</br>
IMPORTANT!!!</br>
Don’t forget to refill your wallet with tokens from the faucet occasionally so you have gas for transactions.</br>
The cooldown between batches of claims is 12 hours and 1 minute.</br>
The delay between individual claims ranges from 5 to 15 seconds.

## To exit the screen session without stopping the script, press ctrl+a, then D.

### https://t.me/layerairdrop - Group
### https://t.me/https://t.me/+UgQeEnnWrodiNTI1 - Chat
