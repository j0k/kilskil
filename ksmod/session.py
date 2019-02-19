class Session:
    def __init__(_):
        _.db = dbdata
        _.rec = Skill()
        _.username = None
        _.reset_state()
        _.reset_action()

    def reset_state(_):
        _.sm      = ActionSM(_)

    def reset_action(_):
        _.input = {"text" : "", "call" : None}
