import httpx
import os


DISCORD_WEBHOOK_URL=os.getenv("DISCORD_WEBHOOK_URL")


async def send_discord_notification(message:str,source:str):
    payload={
        "embeds":[
            {
                "title":"異常検知アラート",
                "color":15158332,
                "fields":[
                    {"name":"送信元(Node)","value":source,"inline":True},
                    {"name":"ログの内容","value":message}
                ],
                "description":"AIモデルが異常なパターンを検知しました。至急確認してください。"
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response=await client.post(DISCORD_WEBHOOK_URL,json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"通知の送信に失敗しました:{e}")
