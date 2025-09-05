import semopy as sem
import matplotlib.pyplot as plt

mod_desc = """
# 测量模型（潜变量 = ~ 观测变量）
Building  =~ history_age + shape_intact + repair_level
Craft     =~ light_clarity + pattern_restore + interact_smooth
Culture   =~ demo_duration + contact_freq
Value     =~ nps_diff + emotion_score
Economy   =~ ticket_will + souvenir_will + study_will
Reproduction =~ monthly_hours + innovate_freq

# 结构模型（潜变量 ~ 潜变量）
Value ~ Building + Craft + Culture
Economy ~ Value
Reproduction ~ Economy
"""

model = sem.Model(mod_desc)

g = sem.plot.semplot(model, "model_graph.png",
                     plot_ests=False,      
                     engine="dot")        
print("已生成")