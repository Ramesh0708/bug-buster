#!/usr/bin/env python3
"""
Bug Buster - A text-based game where players fix AWS configuration errors
"""

import random
import sys
import time
import os

class BugBusterGame:
    def __init__(self):
        self.player_name = ""
        self.score = 0
        self.level = 1
        self.max_levels = 5
        
        # AWS configuration challenges with errors and solutions
        self.challenges = [
            {
                "title": "S3 Bucket Policy Error",
                "description": "Your S3 bucket is not accessible. The policy has an error.",
                "error_config": """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket/*",
            "Condition": {
                "StringNotEquals": {
                    "aws:sourceVpc": "vpc-12345"
                }
            }
        }
    ]
}""",
                "hint": "The Condition is using StringNotEquals which is opposite of what we want.",
                "solution": "StringEquals",
                "explanation": "The policy should use StringEquals to restrict access to the specified VPC."
            },
            {
                "title": "IAM Role Trust Policy",
                "description": "Your Lambda function can't assume its role. The trust policy is incorrect.",
                "error_config": """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}""",
                "hint": "This trust policy allows the wrong AWS service to assume the role.",
                "solution": "lambda.amazonaws.com",
                "explanation": "For a Lambda function, the trust policy should specify lambda.amazonaws.com as the service principal."
            },
            {
                "title": "Security Group Configuration",
                "description": "Your EC2 instance can't be accessed via SSH. The security group is misconfigured.",
                "error_config": """{
    "GroupId": "sg-12345",
    "IpPermissions": [
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0"
                }
            ]
        }
    ]
}""",
                "hint": "The security group is missing a rule for SSH access.",
                "solution": "22",
                "explanation": "SSH uses port 22, which needs to be opened in the security group."
            },
            {
                "title": "CloudFormation Template Error",
                "description": "Your CloudFormation stack fails to create an RDS instance due to a parameter error.",
                "error_config": """Resources:
  MyDB:
    Type: AWS::RDS::DBInstance
    Properties:
      AllocatedStorage: 20
      DBInstanceClass: db.t2.micro
      Engine: mysql
      MasterUsername: admin
      MasterUserPassword: password123
      PubliclyAccessible: true""",
                "hint": "Storing passwords in plaintext in CloudFormation templates is a security risk.",
                "solution": "{{resolve:secretsmanager:MyRDSSecret:SecretString:password}}",
                "explanation": "Use AWS Secrets Manager to securely store and reference database credentials."
            },
            {
                "title": "Lambda Function Configuration",
                "description": "Your Lambda function is timing out when processing large files.",
                "error_config": """resource "aws_lambda_function" "processor" {
  function_name = "file-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x"
  timeout       = 3
  memory_size   = 128
}""",
                "hint": "The Lambda function doesn't have enough time or memory to process large files.",
                "solution": "timeout = 15",
                "explanation": "Increasing the timeout gives the function more time to process large files."
            }
        ]
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def type_text(self, text, delay=0.03):
        """Type text with a delay for a more interactive feel."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def display_intro(self):
        """Display the game introduction."""
        self.clear_screen()
        self.type_text("\n" + "=" * 60, 0.01)
        self.type_text("🐛 WELCOME TO BUG BUSTER 🐛".center(60), 0.05)
        self.type_text("=" * 60, 0.01)
        self.type_text("\nYou are an AWS Cloud Engineer tasked with fixing critical")
        self.type_text("configuration errors before they cause system outages!")
        self.type_text("\nExamine each AWS configuration, identify the error,")
        self.type_text("and provide the correct value to fix the bug.")
        self.type_text("\nGood luck, Bug Buster!\n")
        
        self.player_name = input("Enter your name to begin: ")
        if not self.player_name:
            self.player_name = "Bug Buster"
        
        self.type_text(f"\nWelcome, {self.player_name}! Let's squash some bugs!\n")
        input("Press Enter to start your first challenge...")
    
    def display_challenge(self, challenge):
        """Display a challenge to the player."""
        self.clear_screen()
        self.type_text(f"\n🔍 LEVEL {self.level}: {challenge['title']} 🔍\n", 0.03)
        self.type_text(challenge['description'])
        print("\nCurrent Configuration:")
        print("-" * 60)
        print(challenge['error_config'])
        print("-" * 60)
    
    def check_answer(self, challenge, answer):
        """Check if the player's answer is correct."""
        return answer.strip() == challenge['solution']
    
    def play_level(self):
        """Play a single level of the game."""
        if self.level > self.max_levels:
            self.game_complete()
            return
        
        # Get the current challenge
        challenge = self.challenges[self.level - 1]
        self.display_challenge(challenge)
        
        # Give the player three attempts
        attempts = 3
        while attempts > 0:
            print(f"\nAttempts remaining: {attempts}")
            answer = input("\nWhat's the correct value to fix this bug? ")
            
            if self.check_answer(challenge, answer):
                self.score += 100 * attempts  # More points for fewer attempts
                self.type_text("\n✅ CORRECT! Bug squashed successfully!")
                self.type_text(f"Explanation: {challenge['explanation']}")
                self.type_text(f"\nYou earned {100 * attempts} points!")
                self.level += 1
                input("\nPress Enter to continue...")
                return
            else:
                attempts -= 1
                if attempts > 0:
                    self.type_text("\n❌ That's not quite right. Try again!")
                    print(f"Hint: {challenge['hint']}")
                else:
                    self.type_text("\n❌ Sorry, you've run out of attempts!")
                    self.type_text(f"The correct answer was: {challenge['solution']}")
                    self.type_text(f"Explanation: {challenge['explanation']}")
                    self.level += 1
                    input("\nPress Enter to continue...")
                    return
    
    def display_score(self):
        """Display the current score."""
        self.clear_screen()
        self.type_text("\n" + "=" * 60, 0.01)
        self.type_text(f"CURRENT SCORE: {self.score}".center(60), 0.03)
        self.type_text("=" * 60, 0.01)
        self.type_text(f"\nLevel: {self.level - 1}/{self.max_levels} completed")
        input("\nPress Enter to continue...")
    
    def game_complete(self):
        """Display the game completion screen."""
        self.clear_screen()
        self.type_text("\n" + "*" * 60, 0.01)
        self.type_text("🏆 GAME COMPLETE! 🏆".center(60), 0.05)
        self.type_text("*" * 60, 0.01)
        self.type_text(f"\nCongratulations, {self.player_name}!")
        self.type_text(f"You've completed Bug Buster with a score of {self.score} points!")
        
        # Rank based on score
        max_possible_score = 300 * self.max_levels  # 3 attempts * 100 points * levels
        percentage = (self.score / max_possible_score) * 100
        
        if percentage >= 90:
            rank = "AWS Cloud Architect"
        elif percentage >= 70:
            rank = "Senior Cloud Engineer"
        elif percentage >= 50:
            rank = "Cloud Developer"
        else:
            rank = "Cloud Apprentice"
        
        self.type_text(f"\nYour Bug Buster Rank: {rank}")
        self.type_text("\nThank you for playing Bug Buster!")
        self.type_text("Keep honing your AWS configuration skills!")
        
        play_again = input("\nWould you like to play again? (y/n): ")
        if play_again.lower() == 'y':
            self.__init__()
            self.start_game()
        else:
            self.type_text("\nGoodbye! Come back soon to bust more bugs!")
            sys.exit()
    
    def start_game(self):
        """Start the game."""
        self.display_intro()
        
        while self.level <= self.max_levels:
            self.play_level()
            if self.level <= self.max_levels:
                self.display_score()
        
        # Game is complete
        self.game_complete()

if __name__ == "__main__":
    game = BugBusterGame()
    try:
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing Bug Buster!")
        sys.exit()
