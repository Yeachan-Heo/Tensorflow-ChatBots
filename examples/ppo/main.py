from ppo import PPO

ppo = PPO(token="'1101668170:AAHBnU89Ap-6cLpCIdvIKqfWSDkfi5q4Kvk'",
          is_continous=True,
          state_size=3,
          action_size=1,
          lr_value_net=0.0003,
          lr_policy_net=0.0003,
          updates_n=15,
          sample_size=200,
          batch_size=16,
          total_episodes=2000,
          epsilon=0.2,
          lamda=0.9,
          gamma=0.99
          )
if __name__ == '__main__':
    ppo.set_env("Pendulum-v0")
    ppo()
