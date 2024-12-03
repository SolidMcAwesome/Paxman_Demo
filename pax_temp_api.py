from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPost, EditPost

wp = Client('https://olayinka.net/tise/xmlrpc.php', 'Tise', 'TEOh 8U6k 9UZD OVP8 rq9q qkhl')

def upload():
    t_file = open("P:pax_temp_raw.txt", "r")
    temperatures = t_file.read().split(",")
    t_file.close()

    post_id = 1174  # Paxman Demo Web Post Id
    post = wp.call(GetPost(post_id))
    post.content =  "<p>Temperature: " + str(temperatures[0]) + "°C | " +str(temperatures[1]) + "°F<p>" # Updates page to show current temp
    wp.call(EditPost(post_id, post)) # Edits page with updated content
    print("Data updated; Temperature: " + str(temperatures[0]) + "°C | " +str(temperatures[1]) + "°F")
