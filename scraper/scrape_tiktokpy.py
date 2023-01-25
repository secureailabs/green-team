import asyncio

from tiktokpy import TikTokPy


async def main():
    async with TikTokPy() as bot:
        # # Do you want to get trending videos? You can!
        # trending_items = await bot.trending(amount=5)

        # for item in trending_items:
        #     # ❤️ you can like videos
        #     await bot.like(item)
        #     # or unlike them
        #     await bot.unlike(item)
        #     # or follow users
        #     await bot.follow(item.author.username)
        #     # as and unfollow
        #     await bot.unfollow(item.author.username)

        # 😏 getting user's feed
        user_feed_items = await bot.user_feed(username="justinbieber", amount=5)

        for item in user_feed_items:
            # 🎧 get music title, cover, link, author name..
            print("Music title: ", item.music.title)
            # #️⃣ print all tag's title of video
            print([tag.title for tag in item.challenges])
            # 📈 check all video stats
            print("Comments: ", item.stats.comments)
            print("Plays: ", item.stats.plays)
            print("Shares: ", item.stats.shares)
            print("Likes: ", item.stats.likes)

        # and many other things 😉


asyncio.run(main())