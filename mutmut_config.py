from mutmut import Context


def pre_mutation(context: Context):
    if "chat_bot" in context.filename:
        context.skip = True
