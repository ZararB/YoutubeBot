import instaloader 
from instaloader import Profile, Post
ldr = instaloader.Instaloader()
ldr.interactive_login("memeking410")

posts = ldr.get_hashtag_posts('cat')
