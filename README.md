# inv_from_env
Create an ansible dynamic inventory from an environment variable

Sometime you wnat per-job invnetories. Here is one method of creating them simply taking advantage of the fact you can set an environment variable for an inventory source and use an inventory plugin to read that variable and create a simple host inventory from it.
