# Teaching Guidance: Building Agentic AI Applications with LLMs

## Overview

This document provides comprehensive teaching guidance for instructors delivering the "Building Agentic AI Applications with LLMs" course. It covers strategies for balancing theory and practice, encouraging experimentation, fostering collaboration, and providing real-world context.

## Table of Contents

1. [Balancing Theory and Practice](#balancing-theory-and-practice)
2. [Encouraging Experimentation](#encouraging-experimentation)
3. [Fostering Collaboration](#fostering-collaboration)
4. [Providing Real-World Context](#providing-real-world-context)
5. [Teaching Strategies by Learning Style](#teaching-strategies-by-learning-style)
6. [Managing Classroom Dynamics](#managing-classroom-dynamics)
7. [Adapting to Student Needs](#adapting-to-student-needs)

---

## Balancing Theory and Practice

### The 20-30-40-10 Framework

This course follows a structured time allocation:
- **20% Concept Introduction**: Theoretical foundations
- **30% Demonstration**: Instructor-led examples
- **40% Hands-On Practice**: Student-led labs
- **10% Assessment**: Knowledge checks

### Strategies for Theory (20%)

**Keep It Concise**:
- Focus on essential concepts only
- Avoid tangents and excessive detail
- Use the "need to know" vs "nice to know" filter
- Save deep dives for office hours or supplementary materials

**Make It Visual**:
- Use diagrams to illustrate architectures
- Show flowcharts for decision processes
- Create comparison tables for frameworks
- Use animations for dynamic concepts

**Connect to Practice**:
- Preview how theory applies in labs
- Reference real-world applications
- Show why the theory matters
- Bridge to demonstration phase

**Check Understanding**:
- Ask quick comprehension questions
- Use think-pair-share for complex concepts
- Watch for confused faces
- Adjust pace based on feedback

**Example: Module 1 Theory (18 minutes)**
```
Minutes 0-5: LLM capabilities and limitations
- Quick overview with examples
- Visual: Capability vs limitation chart
- Check: "What's one LLM limitation?"

Minutes 5-10: Agent abstraction
- Task decomposition concept
- Visual: Complex task → subtasks diagram
- Check: "How would you decompose booking a flight?"

Minutes 10-15: Architecture types
- Reactive, deliberative, hybrid
- Visual: Architecture comparison table
- Check: "When would you use reactive?"

Minutes 15-18: Production considerations
- Quick overview of reliability, performance, safety
- Preview: "We'll see these in the demo"
```

### Strategies for Demonstration (30%)

**Show, Don't Just Tell**:
- Live code whenever possible
- Narrate your thought process
- Make mistakes intentionally to show debugging
- Explain why you make each decision

**Build Incrementally**:
- Start with simplest version
- Add complexity step by step
- Show before and after comparisons
- Explain each addition

**Engage Students**:
- Ask "What should we do next?"
- Invite predictions about outcomes
- Encourage questions during demo
- Have students suggest improvements

**Make It Real**:
- Use realistic examples and data
- Show actual API responses
- Demonstrate real error scenarios
- Connect to production use cases

**Example: Module 1 Demo (27 minutes)**
```
Minutes 0-8: Basic agent interaction
- Show API setup and authentication
- Make first API call
- Display response
- Discuss response structure
- Q&A: "What do you notice about the response?"

Minutes 8-18: Error handling
- Intentionally cause API error
- Show crash without error handling
- Add try-except block
- Implement retry logic
- Add exponential backoff
- Q&A: "Why exponential backoff?"

Minutes 18-27: Context management
- Show stateless interaction
- Add conversation history
- Demonstrate multi-turn conversation
- Compare stateless vs stateful
- Q&A: "When would you use each?"
```

### Strategies for Practice (40%)

**Protect This Time**:
- This is the most valuable learning time
- Don't cut it short for more theory or demo
- If running behind, cut theory or demo instead
- Students learn by doing, not watching

**Provide Structure**:
- Clear objectives for the lab
- Step-by-step implementation guide
- Checkpoints to verify progress
- Expected outputs for validation

**Circulate and Support**:
- Move around the room/virtual breakout rooms
- Check in with each student/group
- Identify common issues
- Provide hints, not solutions

**Encourage Exploration**:
- "What happens if you change this?"
- "Try a different approach"
- "Can you make it better?"
- "What edge cases should you test?"

**Facilitate Peer Learning**:
- Pair students with different skill levels
- Encourage asking neighbors for help
- Have students explain their solutions
- Create opportunities for code review

**Example: Module 1 Lab (36 minutes)**
```
Minutes 0-5: Setup and orientation
- Verify everyone has API keys
- Review lab objectives
- Answer setup questions
- Start implementation

Minutes 5-25: Implementation
- Students work independently or in pairs
- Instructor circulates
- Provides hints for common issues
- Encourages experimentation

Minutes 25-30: Testing
- Students test with various inputs
- Try edge cases
- Compare results with neighbors
- Debug any issues

Minutes 30-36: Wrap-up
- Quick demo of working solution
- Discuss challenges encountered
- Share interesting approaches
- Preview next module
```

### Strategies for Assessment (10%)

**Make It Meaningful**:
- Questions should test understanding, not memorization
- Include application and analysis questions
- Use scenarios from real-world contexts
- Align with exam blueprint topics

**Provide Immediate Feedback**:
- Review answers as a group when possible
- Explain why answers are correct/incorrect
- Address common misconceptions
- Use as teaching opportunity

**Use Formatively**:
- Identify topics needing reinforcement
- Adjust future teaching based on results
- Provide additional resources for weak areas
- Celebrate successes

### Balancing Tips

**When Theory Runs Long**:
- Identify what can be moved to reading
- Shorten or combine demonstrations
- Never significantly cut practice time
- Consider flipped classroom approach

**When Practice Needs More Time**:
- Extend lab time if possible
- Assign quiz as homework
- Provide extra office hours
- Create optional extension activities

**When Students Are Struggling**:
- Slow down and reinforce fundamentals
- Provide more scaffolding
- Break problems into smaller steps
- Offer additional practice opportunities

**When Students Are Ahead**:
- Provide extension challenges
- Introduce advanced topics
- Encourage helping others
- Assign independent projects



---

## Encouraging Experimentation

### Creating a Safe Environment

**Normalize Failure**:
- Share your own debugging stories
- Celebrate "productive failures"
- Frame errors as learning opportunities
- Avoid judgment of "wrong" approaches

**Example Phrases**:
- "That's an interesting error - let's figure out why"
- "I make this mistake all the time"
- "Great question - let's explore that together"
- "There's no one right way to do this"

**Reduce Stakes**:
- Labs are for learning, not just grading
- Allow revisions and resubmissions
- Focus on process, not just outcomes
- Provide multiple attempts on quizzes

### Providing Scaffolding

**Start with Working Examples**:
- Provide complete starter code
- Show working reference implementations
- Demonstrate successful patterns
- Build confidence before removing support

**Gradually Remove Support**:
- Early labs: Detailed step-by-step guides
- Middle labs: High-level guidance
- Later labs: Minimal scaffolding
- Final project: Independent work

**Offer Multiple Paths**:
- "You could try approach A or B"
- Provide alternative implementations
- Show different frameworks/tools
- Respect different problem-solving styles

### Facilitating Discovery

**Ask Guiding Questions**:
Instead of: "Add error handling here"
Ask: "What could go wrong at this step?"

Instead of: "Use exponential backoff"
Ask: "How can we avoid overwhelming the API?"

Instead of: "This is wrong"
Ask: "What do you expect to happen? What actually happened?"

**Encourage Hypothesis Testing**:
- "What do you think will happen if...?"
- "How could you test that assumption?"
- "What evidence would support your hypothesis?"
- "Let's try it and see"

**Support Systematic Debugging**:
- "What's the last thing that worked?"
- "Can you isolate the problem?"
- "What have you tried so far?"
- "What does the error message tell us?"

### Experimentation Activities

**"What If" Challenges**:
- "What if we doubled the chunk size?"
- "What if we removed the retry logic?"
- "What if we used a different model?"
- Predict, test, observe, explain

**Code Golf**:
- "Can you solve this in fewer lines?"
- "Can you make it more readable?"
- "Can you make it faster?"
- Multiple valid solutions

**Reverse Engineering**:
- Provide working code without explanation
- Students figure out how it works
- Discuss design decisions
- Identify improvements

**Extension Challenges**:
- "Add a feature that..."
- "Optimize for..."
- "Handle this edge case..."
- "Integrate with..."

### Handling Experimentation Gone Wrong

**When Students Are Stuck**:
1. Ask them to explain what they're trying to do
2. Help them break it into smaller steps
3. Suggest one small thing to try
4. Check back after they try it

**When Experiments Break Things**:
- "Great! Now we know what doesn't work"
- "What did we learn from this?"
- "How can we fix it?"
- Use version control to recover

**When Students Are Frustrated**:
- Acknowledge the difficulty
- Remind them of progress made
- Suggest taking a break
- Offer to work through it together

### Celebrating Experimentation

**Recognize Creative Solutions**:
- "That's a clever approach!"
- "I hadn't thought of that"
- "Can you share that with the class?"
- Feature student work in examples

**Share Discoveries**:
- Create a "cool findings" channel
- Dedicate time for show-and-tell
- Document interesting approaches
- Build a class knowledge base

**Reward Risk-Taking**:
- Extra credit for creative solutions
- Bonus points for trying advanced features
- Recognition for helping others
- Showcase exceptional work

---

## Fostering Collaboration

### Pair Programming

**Benefits**:
- Immediate peer feedback
- Verbalization aids understanding
- Reduces frustration
- Builds communication skills

**Implementation**:
- Assign pairs with complementary skills
- Rotate roles (driver/navigator) every 15-20 minutes
- Rotate partners across modules
- Provide clear role descriptions

**Driver Role**:
- Types the code
- Focuses on syntax and implementation
- Asks questions when unsure
- Follows navigator's guidance

**Navigator Role**:
- Thinks about strategy and design
- Watches for errors
- Suggests approaches
- Asks guiding questions

**Monitoring Pairs**:
- Watch for balanced participation
- Intervene if one person dominates
- Encourage communication
- Provide feedback on collaboration

### Group Discussions

**Think-Pair-Share**:
1. **Think** (2 min): Individual reflection on question
2. **Pair** (3 min): Discuss with partner
3. **Share** (5 min): Share with whole class

**Benefits**:
- Everyone participates
- Rehearse ideas before sharing publicly
- Build confidence
- Generate diverse perspectives

**Jigsaw Method**:
1. Divide topic into subtopics
2. Assign each group a subtopic
3. Groups become "experts"
4. Regroup to teach each other

**Example**: Multi-agent frameworks
- Group 1: LangGraph
- Group 2: CrewAI
- Group 3: AutoGen
- Regroup: Each person teaches their framework

**Fishbowl Discussions**:
- Inner circle discusses topic
- Outer circle observes
- Switch roles
- Debrief on discussion quality

### Peer Learning

**Code Reviews**:
- Students review each other's code
- Provide constructive feedback
- Learn from different approaches
- Practice professional skill

**Code Review Guidelines**:
- Start with positive observations
- Ask questions rather than criticize
- Suggest improvements, don't demand
- Focus on learning, not grading

**Peer Teaching**:
- Advanced students help struggling students
- Benefits both (teaching reinforces learning)
- Builds community
- Develops communication skills

**Study Groups**:
- Encourage formation of study groups
- Provide structure (topics, questions)
- Facilitate connections between students
- Monitor to ensure productivity

### Collaborative Projects

**Team Formation**:
- Mix skill levels
- Consider personality types
- Rotate teams across projects
- Allow some self-selection

**Role Assignment**:
- Architect: Design system
- Developer: Implement features
- Tester: Write tests, find bugs
- Documenter: Write documentation
- Rotate roles across projects

**Collaboration Tools**:
- Git for version control
- GitHub for code sharing
- Slack/Discord for communication
- Shared documents for planning

**Managing Team Dynamics**:
- Set clear expectations
- Provide collaboration rubric
- Monitor progress regularly
- Address conflicts early

### Building Community

**Icebreakers**:
- Share background and interests
- Discuss favorite AI applications
- Share learning goals
- Build connections early

**Class Norms**:
- Respect all questions
- Support each other
- Share knowledge freely
- Celebrate successes together

**Social Activities**:
- Virtual coffee chats
- Coding challenges
- Guest speaker Q&As
- End-of-course celebration

**Online Community**:
- Discussion forum or Slack channel
- Encourage questions and answers
- Share resources and articles
- Continue after course ends

---

## Providing Real-World Context

### Industry Examples

**Production Deployment Stories**:
- Share experiences from real deployments
- Discuss what went wrong and why
- Explain how problems were solved
- Connect to course concepts

**Example Story Template**:
```
Context: Company X needed to deploy agent Y
Challenge: Problem Z occurred
Solution: We tried A, then B, finally C worked
Lesson: Key takeaway for students
Connection: How this relates to Module N
```

**Failure Mode Analysis**:
- Real examples of agent failures
- Hallucinations in production
- Scaling challenges
- Security incidents
- Lessons learned

**Success Stories**:
- Agents that work well in production
- Business impact and metrics
- Technical innovations
- Team and process factors

### Use Case Analysis

**Customer Service Agents**:
- Architecture decisions
- Handling high volume
- Maintaining quality
- Measuring success
- Continuous improvement

**Research Assistants**:
- Information retrieval challenges
- Synthesis and summarization
- Citation and attribution
- Accuracy validation
- User trust

**Code Assistants**:
- Codebase understanding
- Context management
- Code generation quality
- Security considerations
- Developer adoption

**Meeting Companions**:
- Real-time processing
- Multi-speaker handling
- Action item extraction
- Privacy concerns
- Integration challenges

### Business Context

**Requirements Gathering**:
- How to understand business needs
- Translating to technical requirements
- Managing stakeholder expectations
- Balancing constraints

**Cost-Benefit Analysis**:
- Development costs
- Infrastructure costs
- Maintenance costs
- Business value
- ROI calculation

**Risk Assessment**:
- Technical risks
- Business risks
- Regulatory risks
- Mitigation strategies
- Risk-reward trade-offs

### Ethical and Societal Context

**Responsible AI**:
- Real examples of AI harm
- Bias in production systems
- Privacy violations
- Accountability challenges
- Best practices

**Regulatory Landscape**:
- GDPR implications
- HIPAA requirements
- Industry-specific regulations
- Compliance strategies
- Future trends

**Societal Impact**:
- Job displacement concerns
- Accessibility benefits
- Environmental costs
- Digital divide
- Long-term implications

### Connecting to Current Events

**Recent Developments**:
- New model releases
- Platform updates
- Research breakthroughs
- Industry trends
- Regulatory changes

**Discussion Prompts**:
- "What do you think about [recent news]?"
- "How does this relate to what we're learning?"
- "What are the implications?"
- "How might this change the field?"

### Guest Speakers

**Practitioner Talks**:
- Invite industry practitioners
- Share real-world experiences
- Q&A sessions
- Networking opportunities

**Topics to Cover**:
- Day-to-day work
- Career paths
- Skills needed
- Challenges faced
- Advice for students

**Preparation**:
- Brief speaker on audience
- Provide course context
- Suggest topics
- Prepare students with questions
- Follow up with discussion

### Industry Resources

**Documentation**:
- NVIDIA official docs
- Framework documentation
- Best practice guides
- Architecture patterns

**Research Papers**:
- Foundational papers
- Recent advances
- Practical applications
- Critical analyses

**Blogs and Articles**:
- Company engineering blogs
- Practitioner experiences
- Tutorial and how-tos
- Industry analysis

**Conferences and Events**:
- NeurIPS, ICML, ACL
- Industry conferences
- Local meetups
- Virtual events

---

## Teaching Strategies by Learning Style

### Visual Learners

**Strategies**:
- Use diagrams and flowcharts extensively
- Create visual comparisons (tables, charts)
- Show code with syntax highlighting
- Use color coding for concepts
- Provide architecture diagrams

**Activities**:
- Draw system architectures
- Create concept maps
- Visualize data flows
- Watch video demonstrations
- Use interactive visualizations

### Auditory Learners

**Strategies**:
- Narrate demonstrations thoroughly
- Encourage verbal explanations
- Use discussions and debates
- Provide audio recordings of lectures
- Facilitate group discussions

**Activities**:
- Explain concepts to partners
- Participate in discussions
- Listen to podcasts
- Attend guest speaker talks
- Verbal code walkthroughs

### Kinesthetic Learners

**Strategies**:
- Maximize hands-on practice time
- Use physical analogies
- Encourage experimentation
- Provide immediate feedback
- Allow movement and breaks

**Activities**:
- Code along with demonstrations
- Build projects
- Debug real problems
- Experiment with parameters
- Pair programming

### Reading/Writing Learners

**Strategies**:
- Provide comprehensive written materials
- Assign reading and writing tasks
- Use code comments extensively
- Encourage note-taking
- Provide written examples

**Activities**:
- Read documentation
- Write technical reports
- Create documentation
- Take detailed notes
- Write blog posts about learning

### Multi-Modal Approach

**Best Practice**: Combine multiple modalities
- Visual: Show diagram
- Auditory: Explain verbally
- Kinesthetic: Have students build it
- Reading/Writing: Provide written summary

**Example: Teaching RAG**:
1. **Visual**: Show RAG pipeline diagram
2. **Auditory**: Explain each component
3. **Kinesthetic**: Build RAG pipeline in lab
4. **Reading/Writing**: Read documentation, write reflection



---

## Managing Classroom Dynamics

### Handling Different Personalities

**The Quiet Student**:
- Call on gently with easy questions
- Use think-pair-share to build confidence
- Provide written response options
- Create small group opportunities
- Acknowledge contributions warmly

**The Dominant Voice**:
- "Let's hear from someone who hasn't spoken"
- Use structured turn-taking
- Redirect questions to others
- Speak privately if needed
- Channel energy into helping others

**The Skeptic**:
- Acknowledge valid concerns
- Provide evidence and examples
- Invite constructive criticism
- Use as devil's advocate
- Don't take it personally

**The Perfectionist**:
- Emphasize learning over perfection
- Share your own mistakes
- Set realistic expectations
- Celebrate progress
- Encourage "good enough" mindset

**The Struggling Student**:
- Provide extra support
- Break problems into smaller steps
- Offer office hours
- Connect with resources
- Monitor for deeper issues

### Managing Energy Levels

**High Energy**:
- Channel into productive activities
- Use interactive exercises
- Encourage peer teaching
- Provide challenging extensions
- Maintain structure

**Low Energy**:
- Take breaks
- Use energizers (quick activities)
- Vary teaching methods
- Connect to interests
- Check for underlying issues

**Mixed Energy**:
- Pair high and low energy students
- Alternate active and passive activities
- Provide choice in activities
- Monitor and adjust

### Handling Difficult Situations

**Technical Failures**:
- Stay calm and positive
- Have backup plans ready
- Use as teaching moment
- Acknowledge frustration
- Move forward quickly

**Disruptive Behavior**:
- Address privately when possible
- Set clear expectations
- Be consistent with consequences
- Focus on behavior, not person
- Seek support if needed

**Conflicts Between Students**:
- Address early
- Listen to all perspectives
- Focus on resolution
- Teach conflict resolution skills
- Follow up to ensure resolution

**Student Complaints**:
- Listen without defensiveness
- Acknowledge concerns
- Explain rationale
- Seek solutions together
- Follow up on commitments

### Building Positive Culture

**Set Tone Early**:
- First class sets expectations
- Model desired behavior
- Establish norms together
- Create welcoming environment
- Build relationships

**Maintain Consistency**:
- Follow through on commitments
- Apply rules fairly
- Be predictable
- Communicate clearly
- Admit mistakes

**Celebrate Successes**:
- Acknowledge progress
- Recognize effort
- Share achievements
- Create success stories
- Build momentum

**Address Issues Promptly**:
- Don't let problems fester
- Be proactive
- Communicate directly
- Seek solutions
- Follow up

---

## Adapting to Student Needs

### Assessing Student Readiness

**Pre-Course Assessment**:
- Survey background and experience
- Test prerequisite knowledge
- Identify learning goals
- Understand constraints
- Plan accordingly

**Ongoing Assessment**:
- Monitor quiz performance
- Observe lab progress
- Check in individually
- Use formative assessments
- Adjust as needed

### Differentiation Strategies

**For Advanced Students**:
- Provide extension challenges
- Introduce advanced topics
- Assign mentoring roles
- Offer independent projects
- Connect to research

**For Struggling Students**:
- Provide additional scaffolding
- Break down concepts further
- Offer extra practice
- Schedule office hours
- Connect to resources

**For Students with Different Backgrounds**:
- Provide context for unfamiliar concepts
- Use diverse examples
- Offer multiple explanations
- Connect to prior knowledge
- Be patient with learning curves

### Flexible Pacing

**When to Slow Down**:
- Many students struggling
- Foundational concepts unclear
- Quiz scores low
- Lab completion rates low
- Student feedback indicates

**When to Speed Up**:
- Students ahead of schedule
- Concepts well-understood
- High engagement
- Strong performance
- Student feedback indicates

**How to Adjust**:
- Move content to reading
- Combine related topics
- Extend or shorten labs
- Add or remove examples
- Adjust homework

### Accommodations

**Learning Disabilities**:
- Extended time on assessments
- Alternative assessment formats
- Note-taking support
- Assistive technology
- Flexible deadlines

**Language Barriers**:
- Provide written materials
- Allow extra processing time
- Use visual aids
- Encourage questions
- Offer translation resources

**Technical Constraints**:
- Provide alternative access
- Record sessions
- Offer offline options
- Flexible attendance
- Asynchronous options

### Supporting Diverse Learners

**Different Career Goals**:
- Connect content to various paths
- Provide diverse examples
- Offer choice in projects
- Respect different motivations
- Support individual goals

**Different Learning Paces**:
- Provide self-paced options
- Offer additional resources
- Allow flexible deadlines
- Support both fast and slow learners
- Focus on mastery, not speed

**Different Prior Knowledge**:
- Provide prerequisite resources
- Offer review sessions
- Create study groups
- Pair students strategically
- Adjust expectations appropriately

---

## Continuous Improvement

### Reflecting on Teaching

**After Each Class**:
- What went well?
- What could be improved?
- Did students understand?
- Was timing appropriate?
- What will I change next time?

**After Each Module**:
- Review quiz results
- Analyze lab completion
- Read student feedback
- Identify patterns
- Plan adjustments

**After Course**:
- Comprehensive review
- Student outcomes analysis
- Certification pass rates
- Long-term impact
- Major revisions needed

### Gathering Feedback

**Informal Feedback**:
- Quick pulse checks
- Observation of engagement
- One-on-one conversations
- Body language and energy
- Participation levels

**Formal Feedback**:
- Mid-course surveys
- End-of-course evaluations
- Focus groups
- Anonymous feedback forms
- Exit interviews

**Acting on Feedback**:
- Identify actionable items
- Prioritize changes
- Communicate changes to students
- Implement improvements
- Follow up on impact

### Professional Development

**Stay Current**:
- Follow NVIDIA updates
- Read research papers
- Attend conferences
- Take courses
- Experiment with new tools

**Improve Teaching Skills**:
- Attend teaching workshops
- Observe other instructors
- Join teaching communities
- Read pedagogy literature
- Seek mentorship

**Build Network**:
- Connect with other instructors
- Join professional organizations
- Participate in forums
- Share experiences
- Learn from others

---

## Conclusion

Effective teaching of agentic AI requires balancing multiple considerations:

**Theory and Practice**: Provide solid foundations while maximizing hands-on learning

**Structure and Flexibility**: Follow the curriculum while adapting to student needs

**Challenge and Support**: Set high standards while providing appropriate scaffolding

**Individual and Collaborative**: Support individual learning while fostering community

**Content and Context**: Teach technical skills while connecting to real-world applications

### Keys to Success

1. **Know Your Students**: Understand their backgrounds, goals, and needs
2. **Be Flexible**: Adapt to circumstances while maintaining standards
3. **Stay Current**: Keep up with rapidly evolving field
4. **Build Community**: Create supportive learning environment
5. **Reflect and Improve**: Continuously refine your teaching

### Remember

- You're not just teaching content, you're developing practitioners
- Every student learns differently - be patient and adaptable
- Real-world context makes concepts memorable and meaningful
- Hands-on practice is where real learning happens
- Your enthusiasm and passion are contagious

### Final Thoughts

Teaching this course is an opportunity to shape the next generation of agentic AI practitioners. By balancing theory and practice, encouraging experimentation, fostering collaboration, and providing real-world context, you'll help students develop not just technical skills, but the mindset and approaches needed for success in this rapidly evolving field.

Your role is to guide, support, challenge, and inspire. The impact you have extends far beyond the classroom, influencing how students approach problems, build systems, and contribute to the field throughout their careers.

Good luck, and enjoy the journey!

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**For**: Building Agentic AI Applications with LLMs  
**Aligned with**: NCP-AAI Exam Blueprint v1.0

