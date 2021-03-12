msg_template = """Hello {name}, welcome to {website}. We are happy to have
you here with us. Hope you will enjoy our content!
"""

def format_msg(name="Jose", website="memorium.live"):
    my_msg = msg_template.format(name=name, website=website)
    #print(my_msg)
    return my_msg

