class Quete : 
    def __init__(self, recompense, conditions = None):
        self.conditions = conditions if conditions is not None else {}
        self.recompense = recompense  

    def remplit (self, player) :
        for cond_name, cond_nb  in self.conditions.items() :
            if player.inventaire.items[cond_name][1] < cond_nb:
                return False
        return True 
    
    def recupere_recompense (self, player, recompense_item):
        """Recupère les objets en condition et donne récompense"""
        for cond_name, cond_nb  in self.conditions.items() :
            player.inventaire.retire_item(cond_name, cond_nb)
        player.inventaire.ajoute_item(recompense_item)