
# How to use

Copy `.env.example` to `.env`

`cp .env.example .env`

# How to find Discord Authorization

Login discord with web browser

Open Developer tool (F11 / F22 / Use Inspect Element)

Select the fetch/xhr filter then select one of the urls and look at the headers to see the discord authorization. Then copy and fill in the .env file

# How to find channel id

Go to one of the channels on the discord server and copy the link to one of the messages.

For example as below

`https://discord.com/channels/885705689350144010/971373217002438737/1236861681200664637`

The channel id is `971373217002438737` and paste in the program.