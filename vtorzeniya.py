from snort import Snort

snort_obj = Snort()


# Устанавливаем правила
rules = """
alert tcp any any -> any any (msg:"Suspicious Activity"; sid:1000000; rev:1;)
"""
snort_obj.set_rules(rules)

# Начинаем мониторинг трафика
snort_obj.start()