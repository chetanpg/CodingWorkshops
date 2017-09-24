#Authos Chetan Gavankar
#Goal:- This proram will take the participants and form a team of 4 dependng on the number of lines of code written
#       by them. this will insure that each team has mix of senior and junior developers
from __future__ import unicode_literals
import sys
import statistics



from prompt_toolkit import prompt, AbortAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
import meetup.api


command_completer = WordCompleter(['add'], ignore_case=True)
command_completer = WordCompleter(['list'], ignore_case=True)
command_completer = WordCompleter(['team'], ignore_case=True)
command_completer = WordCompleter(['get_names'], ignore_case=True)

def get_names():
    client = meetup.api.Client('3f6d3275d3b6314e73453c4aa27')

    rsvps=client.GetRsvps(event_id='239174106', urlname='_ChiPy_')
    member_id = ','.join([str(i['member']['member_id']) for i in rsvps.results])
    members = client.GetMembers(member_id=member_id)

    names = []
    for member in members.results:
        try:
            names.append(member['name'])
        except:
            pass # ignore those who do not have a complete profile
#    print(names)
    return names

#command execution ADD/LIST/TEAM/GET_NAMES
def execute(command,participants):

    if command=="get_names":
        names=get_names()
        print(names)
        return

    participant={}
    parms=command.split(",")
    cnt=len(parms)
#implement add command
#if add,chetan,30 is typed on the terminal
    if (cnt == 3):
        for pos,parm in enumerate(parms):
             if pos == 0:
                 if parm != "ADD" and parm != "add":
                   print("ADD command missing Try Again:(ADD,<full name>,<number of Python written>)"+ command)
#if lines coded is not numeric value
             if pos == 2:
                  if parm.isdigit():
                      lines=parm
                  else:
                      print("Number of lines not numeric Try Again:(ADD,<full name>,<number of Python written>)"+ command)
             if pos == 1:
                  name=parm
#add all participant
        participant[name] = lines
        participants.append(participant)
#        print(participants)
#        return "You issued:" + command
    else:
#implement list command
        if (cnt == 1) and (command == "list" or command == "LIST"):
             print("Listing all added participants:")
             print("=====================================================================\n")
             print("Developer             Number of lines of code written:\n")
             print("=====================================================================\n")
             med=[]
             total=0
             for count,participant in enumerate(participants):
                 if isinstance(participant, dict):
                   for key,value in participant.items():
                      med.append(int(value))
                      print("%s %50s\n" %(key,value))
                   total=count+1
                 else:
                    print("Wrong Command Try Again:(ADD,<full name>,<number of Python written>)"+ command)
             if (total) > 0:
                med_lines = statistics.median(med)
                print("Total Pariticipants:%s \n" %(total))
                print("Median Number of Lines of code written :%s \n" %(med_lines))
             else:
                print("Pariticipants Not Added Yet\n")
        else:
#implement team command
             if (cnt == 1) and (command == "team" or command == "TEAM"):
                med=[]
                for count,participant in enumerate(participants):
                     for key,value in participant.items():
                            med.append(int(value))
                med_lines = statistics.median(med)
                below_median=[]
                above_median=[]
                form_group(participants,med_lines,below_median,above_median)
                print("Above and Below Median Groups Formed\n")
                print(below_median)
                print(above_median)
                bigger_group=[]
                smaller_group=[]
#the way team form function works , the outer loop needs to be > inner loop or equal
#that's why following code is taking care of passing bigger and smaller groups accordingly
                if len(below_median) > len(above_median):
                    bigger_group = below_median
                    smaller_group = above_median
                else:
                    bigger_group  = above_median
                    smaller_group = below_median
#function to form teams
                form_teams(bigger_group,smaller_group)
             else:
                  print("Wrong Command Try Again:(ADD,<full name>,<number of Python written>)"+ command)

#implement team build logic here
def form_group(participants,med_lines,below_median,above_median):
    total=len(participants)
    if (total) > 0:
#if number particiapants less than 5 , then only one team is formed
        if total < 5:
            grp=[]
            group={}
            for participant in participants:
                for key,value in participant.items():
                     grp.append(key)
            group["Team1"] = grp
            print(group)
        else:
            if total > 4:
               for participant in participants:
                   for key,value in participant.items():
                        if int(value) > int(med_lines):
                           above_median.append(key)
                        else:
                           below_median.append(key)
    else:
        print("No participant added yet"+command)

#logic to form teams from two groups created , one > median and other < median value
def form_teams(bigger_group,smaller_group):
#this code create a new list by taking 1 element from group1 and same element position from 2nd group and remaining elements will be
#inserted into the list at the bottom
    group1=bigger_group
    group2=smaller_group
    new_order=[]
    for i in range(len(group1)):
       limit= len(group2)
       if i < limit:
         for j in range(i,len(group2)):
            if i==j:
                   new_order.append(group1[i])
                   new_order.append(group2[j])
       else:
         new_order.append(group1[i])

    print("Combination of members above/below median Groups\n")
    for name in new_order:
       print(name)
#one the above code form the list of mmebers in required order then only logic needed is to pick 4 members at a time to form group and remaining one will
#will be put in new team
    team_count=0
    members=[]
    all_teams=[]
    team={}
    for count,name in enumerate(new_order):
        mem_count=count+1
        if mem_count == 4:
           print("test:"+name)
           team_count=team_count+1
           team_name= "TEAM"+ str(team_count)
           members.append(name)
           team[team_name] = members
           mem_count=0
           all_teams.append(team)
           team={}
           members=[]
        else:
            members.append(name)
            max=count+1
            if max == len(new_order):
                team_count=team_count+1
                team_name= "TEAM"+ str(team_count)
                team[team_name] = members
                all_teams.append(team)

#print the teams formed
    for teams in all_teams:
      for key,value in teams.items():
         print("Team Name:%s Developers:%0s\n" %(key,value))


def main():
    history = InMemoryHistory()
    participants = []
    med_lines=0
    while True:
        try:
            text = prompt('> ',
                          completer = command_completer,
                          history=history,
                          on_abort=AbortAction.RETRY)
            execute(text,participants)
        except EOFError:
            break  # Control-D pressed.

    print('GoodBye!')

if __name__ == '__main__':
    main()
